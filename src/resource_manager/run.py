from api import *
    
def run_resource_manager():
    run_api()
    print("RM is running")

run_resource_manager()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)