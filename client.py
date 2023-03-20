# client.py

import grpc

import user_info_pb2
import user_info_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = user_info_pb2_grpc.UserInfoServiceStub(channel)
        email = input("Enter email: ")
        response = stub.GetUserInfo(user_info_pb2.GetUserInfoRequest(email=email))
        print("Name: {}".format(response.name))
        print("Phone: {}".format(response.phone))
        print("Address: {}".format(response.address))

if __name__ == "__main__":
    run()
