import requests


def run_query(query, headers):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {0}. {1}".format(request.status_code, \
            query))


if __name__ == '__main__':
    headers = {"Authorization": "token 3edbeb13fc20a225a00de809867acd3caf7edec7"}

    for lang in ["Java", "C", "Python", "C++", "C#", "JavaScript", "PHP", "Swift", "Objective-C", "Ruby", \
            "Groovy", "Go", "Perl", "R", "Lua", "Scala", "Rust", "Haskell", "Clojure", "shell"]:
        query = """
                {{
                  search(query: "language:{0} stars:>500", type: REPOSITORY, first: 100) {{
                    repositoryCount
                    edges {{
                      node {{
                        ... on Repository {{
                          name
                          description
                          url
                          stargazers {{
                            totalCount
                          }}
                          forks {{
                            totalCount
                          }}
                          updatedAt
                          defaultBranchRef {{
                            name
                            target {{
                              ... on Commit {{
                                id
                                history(first: 0) {{
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
    total_count1 = result["data"]["search"]["edges"][0]["node"]["defaultBranchRef"]["target"]["history"]["totalCount"]
    print("Total Count Gson - {}".format(total_count1))
#     print(result)
