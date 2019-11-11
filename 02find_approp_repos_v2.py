import requests


def run_query(query, headers):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {0}. {1}".format(request.status_code,
                                                                                   query))


if __name__ == '__main__':
    headers = {"Authorization": "token fa6ec218cf26b4fb957abd555fd516f24411e27e"}

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
                        }}
                      }}
                    }}
                  }}
                }}
                """.format(lang)

        result1 = run_query(query1, headers)
        count_each_lang = 0
        for edge in result1["data"]["search"]["edges"]:
            stars = edge["node"]["stargazers"]["totalCount"]
            name = edge["node"]["name"]
            owner = edge["node"]["owner"]["login"]
            url = edge["node"]["url"]
            description = edge["node"]["description"]

            query2 = """
                     query {{repository(owner: "{0}", name: "{1}") {{
                       name
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
                     """.format(owner, name)

            result2 = run_query(query2, headers)
            commits = result2["data"]["repository"]["defaultBranchRef"]["target"]["history"]["totalCount"]
            if commits > 2000 and (description is None or "book" not in description.lower()):
                count_each_lang += 1
                with open("E:\\experimentalData\\repo_star500_commit2000_list.txt", "a", encoding='utf8') as f:
                    f.write(("{}\t{}\t{}\t{}\t{}\t{}\t{}\n").format(lang, name, owner, stars, commits,
                                                                    url, description))
        with open("E:\\experimentalData\\repo_star500_commit2000_list.txt", "a", encoding='utf8') as f:
            f.write(("NOTICE: {} programming language -- {} repotories.\n").format(lang, count_each_lang))
        print(("NOTICE: {} programming language -- {} repotories.").format(lang, count_each_lang))
