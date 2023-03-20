# server.py

from concurrent import futures
import grpc
import neo4j

import user_info_pb2
import user_info_pb2_grpc

class UserInfoServicer(user_info_pb2_grpc.UserInfoServiceServicer):
    def __init__(self):
        self._driver = neo4j.GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

    def GetUserInfo(self, request, context):
        email = request.email
        with self._driver.session() as session:
            result = session.run("MATCH (u:User {email: $email}) RETURN u.name as name, u.phone as phone, u.address as address", email=email)
            record = result.single()
            return user_info_pb2.GetUserInfoResponse(
                name=record["name"],
                phone=record["phone"],
                address=record["address"]
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_info_pb2_grpc.add_UserInfoServiceServicer_to_server(UserInfoServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
