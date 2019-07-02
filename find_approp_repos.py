import requests


headers = {"Authorization": "token 5247e606725afbecaee346ebcaaca3990b0b7b21"}


def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {0}. {1}".format(request.status_code, \
                query))


query = """
        {
          gson: repository(owner: "google", name: "gson") {
            ...RepoFragment
          }
          martian: repository(owner: "google", name: "martian") {
            ...RepoFragment
          }
          keyboard: repository(owner: "jasonrudolph", name: "keyboard") {
            ...RepoFragment
          }
        }

        fragment RepoFragment on Repository {
          name
          refs(first: 100, refPrefix: "refs/heads/") {
            edges {
              node {
                name
                target {
                  ... on Commit {
                    id
                    history(first: 0) {
                      totalCount
                    }
                  }
                }
              }
            }
          }
        }
        """

result = run_query(query)
total_count_gson = result["data"]["gson"]["refs"]["edges"][0]["node"]["target"]["history"]["totalCount"]
print("Total Count Gson - {}".format(total_count_gson))
