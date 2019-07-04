import requests


def run_query(query, headers):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {0}. {1}".format(request.status_code, \
            query))


if __name__ == '__main__':
    headers = {"Authorization": "token ec342ee42b85ef86ff276e1f45256aa50fc0f981"}

    with open("/srv/bug_repos/repo_star500_commit2000_list.txt", "w") as f:
        f.write("LANGUAGE\tNAME\tOWNER\tSTARS\tCOMMITS\tURL\tDESCRIPTION\n")
    for lang in ["C", "C++", "Ruby"]:  # C, C++, Ruby
        query1 = """
                {{
                  search(query: "language:{0} stars:>500", type: REPOSITORY, first: 100) {{
                    repositoryCount
                    edges {{
                      node {{
                        ... on Repository {{
                          name
                          owner {{
                            login
                          }}
                          description
                          url
                          stargazers {{
                            totalCount
                          }}
                          defaultBranchRef {{
                            name
                            target {{
                              ... on Commit {{
                                history {{
                                  totalCount
                                }}
                              }}
                            }}
                          }}
                        }}
                      }}
                    }}
                  }}
                }}
                """.format(lang)
        query1 = """
                {{
                  search(query: "language:{0} stars:>500", type: REPOSITORY, first: 100) {{
                    repositoryCount
                    edges {{
                      node {{
                        ... on Repository {{
                          name
                          owner {{
                            login
                          }}
                          description
                          url
                          stargazers {{
                            totalCount
                          }}
                          defaultBranchRef {{
                            name
                            target {{
                              ... on Commit {{
                                history {{
                                  totalCount
                                }}
                              }}
                            }}
                          }}
                        }}
                      }}
                    }}
                  }}
                }}
                """.format(lang)
                    
        result = run_query(query, headers)
        # print(result)
        count_each_lang = 0
        for edge in result["data"]["search"]["edges"]:
            stars = edge["node"]["stargazers"]["totalCount"]
            name = edge["node"]["name"]
            owner = edge["node"]["owner"]["login"]
            url = edge["node"]["url"]
            description = edge["node"]["description"]
            commits = edge["node"]["defaultBranchRef"]["target"]["history"]["totalCount"]
            if commits > 2000 and (description is None or "book" not in description.lower()):
                count_each_lang += 1
                with open("/srv/bug_repos/repo_star500_commit2000_list.txt", "a") as f:
                    f.write(("{}\t{}\t{}\t{}\t{}\t{}\t{}\n").format(lang, name, 
                        owner, stars, commits, url, description))
        with open("/srv/bug_repos/repo_star500_commit2000_list.txt", "a") as f:
            f.write(("NOTICE: {} programming language -- {} repotories.\n").format(lang, count_each_lang))
        print(("NOTICE: {} programming language -- {} repotories.").format(lang, count_each_lang))
