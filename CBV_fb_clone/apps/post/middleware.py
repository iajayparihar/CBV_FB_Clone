
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import datetime
        current_time = datetime.datetime.now()
        # Code to be executed before the view is called
        with open("logdata.txt", 'a') as file:
            file.write(str(current_time) + '\t' + "user : " + str(request.user) + "path : "+ str(request.path) +"\n")
        response = self.get_response(request)
        # Code to be executed after the view is called
        return response