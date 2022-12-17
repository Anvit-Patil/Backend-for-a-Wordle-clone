import requests



def post_to_leaderboard(data, url):
    print("Hello-------------------------------------------------------------------------")
    print(data)
    print(url)

    response = requests.post(url, data = data)
    # app.logger.info(response)
    # if (response.status_code == 200):
    #     print("The request was a success!")
    #     # Code here will only run if the request is successful
    # elif (response.status_code == 404):
    #     print("Result not found!")
    #     # Code here will react to failed requests
