import requests, time, re
from repository import Repository


def run_query(query, headers):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    # while request.status_code == 403 or request.status_code == 502:
    while request.status_code != 200:
        print("WRONG STATUS CODE - {}".format(request.status_code))
        time.sleep(5)
        request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    
    if request.status_code != 200:
        raise Exception("Query failed to run by returning code of {0}. {1}".format(request.status_code,
                                                                                   query))
    return request.json()


if __name__ == '__main__':
    REPOS_DIR_PRE = "/srv/bug_repos"

    with open("/srv/bug_repo_info/selected/selected_repos.txt", "r") as f:
        for line in f:
            if line[:6] != "NOTICE" and line[:8] != "LANGUAGE":
                repo = Repository(line.strip())
            else:
                print(line)
                continue

            headers = {"Authorization": "token 1ddd5ca713b08eed6c014c620b932ee73fbdedfd"}
            end_cursor = "null"
            has_next_page = True
            flag = True

            with open("/srv/bug_repo_info/selected/pr/{0}_{1}_{2}.txt".format(repo.language, repo.owner, 
                                                                             repo.name), "w") as f:
                f.write("NUMBER\tTITLE\tAUTHER\tCREATE_TIME\tMERGE_COMMIT\tDESCRIPTION\t" + 
                        "FIRST_COMMENT_AUTHER\tFIRST_COMMENT_TIME\tFIRST_COMMENT\n")

            while has_next_page:
                query = """
                        query {{repository(owner: "{0}", name: "{1}") {{
                          name
                          pullRequests(after: {2}, first: 100, states: MERGED) {{
                            edges {{
                              node {{
                                number
                                merged
                                title
                                bodyText
                                createdAt
                                author {{
                                    login
                                }}
                                comments(first: 1) {{
                                  edges {{
                                    node {{
                                      author {{
                                        login
                                      }}
                                      authorAssociation
                                      createdAt
                                      bodyText
                                    }}
                                  }}
                                }}
                                mergeCommit {{
                                  abbreviatedOid
                                }}
                                timelineItems(first: 10, itemTypes: [MERGED_EVENT]) {{
                                    nodes {{
                                      ... on MergedEvent {{
                                        commit {{
                                          abbreviatedOid
                                        }}
                                      }}
                                    }}
                                }}
                              }}
                            }}
                            pageInfo {{
                              endCursor
                              hasNextPage
                            }}
                          }}
                        }}}}
                        """.format(repo.owner, repo.name, end_cursor if flag else '"' + end_cursor + '"')
                flag = False
                result = run_query(query, headers)
                if list(result.keys())[0] != "data":
                    print(repo.language + " - " + repo.owner + " - " + repo.name + " - " + str(result))
                    continue
                for edge in result["data"]["repository"]["pullRequests"]["edges"]:
                    number = edge["node"]["number"]
                    title = edge["node"]["title"]
                    if not edge["node"]["author"]:
                        author = "ghost"
                    else:
                        author = edge["node"]["author"]["login"]
                    description = edge["node"]["bodyText"]
                    create_time = edge["node"]["createdAt"]
                    # merge_commit = edge["node"]["mergeCommit"]["abbreviatedOid"]
                    if edge["node"]["timelineItems"]["nodes"] and edge["node"]["timelineItems"]["nodes"][0]["commit"]:
                        merge_commit = edge["node"]["timelineItems"]["nodes"][0]["commit"]["abbreviatedOid"]
                    else:
                        merge_commit = "None"
                        with open("/srv/bug_repo_info/pull_request/error_log.txt", "a") as f:
                            f.write("{0}\t{1}\t{2}\t{3}\n".format(repo.language, repo.url, number, title))
                        print(str(number) + " - " + title)

                    if edge["node"]["comments"]["edges"]:
                        first_comment = edge["node"]["comments"]["edges"][0]["node"]["bodyText"]
                        if edge["node"]["comments"]["edges"][0]["node"]["author"]:
                            first_comment_author = edge["node"]["comments"]["edges"][0]["node"]["author"]["login"]
                        else:
                            first_comment_author = "ghost"
                        first_comment_time = edge["node"]["comments"]["edges"][0]["node"]["createdAt"]
                    else:
                        first_comment = ""
                        first_comment_author = ""
                        first_comment_time = ""

                    title = re.sub(r"\s+", " ", title)
                    author = re.sub(r"\s+", " ", author)
                    description = re.sub(r"\s+", " ", description)
                    first_comment_author = re.sub(r"\s+", " ", first_comment_author)
                    first_comment = re.sub(r"\s+", " ", first_comment)

                    with open("/srv/bug_repo_info/selected/pr/{0}_{1}_{2}.txt".format(repo.language, repo.owner, repo.name),
                              "a") as f:
                        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                            number, title, author, create_time, merge_commit, description, 
                            first_comment_author, first_comment_time, first_comment))
                end_cursor = result["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]
                has_next_page = result["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]
                print(repo.name + " - " + str(has_next_page))
