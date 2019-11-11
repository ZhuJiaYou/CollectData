import requests


def run_query(query, headers):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {0}. {1}".format(request.status_code, \
            query))


if __name__ == '__main__':
    headers = {"Authorization": "token fa6ec218cf26b4fb957abd555fd516f24411e27e"}

    with open("E:\\experimentalData\\repo_star500_commit2000_list.txt", "w", encoding='utf8') as f:
        f.write("LANGUAGE\tNAME\tOWNER\tSTARS\tCOMMITS\tURL\tDESCRIPTION\n")
    for lang in ["Java", "Python", "C#", "JavaScript", "PHP", "Swift", "Objective-C", "Groovy", "Go", \
            "Perl", "R", "Lua", "Scala", "Rust", "Haskell", "Clojure", "shell"]:  # C, C++, Ruby
        query = """
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
                with open("E:\\experimentalData\\repo_star500_commit2000_list.txt", "a", encoding='utf8') as f:
                    f.write(("{}\t{}\t{}\t{}\t{}\t{}\t{}\n").format(lang, name, 
                        owner, stars, commits, url, description))
        with open("E:\\experimentalData\\repo_star500_commit2000_list.txt", "a", encoding='utf8') as f:
            f.write(("NOTICE: {} programming language -- {} repotories.\n").format(lang, count_each_lang))
        print(("NOTICE: {} programming language -- {} repotories.").format(lang, count_each_lang))
