from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Book
from .serializers import BookSerializer

from rest_framework import generics, status

#class BookListApiView(generics.ListAPIView):
   # queryset = Book.objects.all()
   # serializer_class = BookSerializer

class BookListApiView(APIView):

    def get (self, reqquest):
        books = Book.objects.all()
        serializer_data = BookSerializer(books, many=True)
        data= {
            "status": f"Returned {len(books)} books",
            "books": serializer_data.data
        }

        return Response(data)


#class BookDetailApiView(generics.RetrieveAPIView):
#    queryset = Book.objects.all()
#    serializer_class = BookSerializer

class BookDetailApiView(APIView):

    def get(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
            serializer_data = BookSerializer(book).data

            data= {
                "status": "Successfull",
                "book": serializer_data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"status": "Error",
                 "message": "Book not found"},
            )


#class BookDeleteApiView(generics.DestroyAPIView):
#    queryset = Book.objects.all()
#    serializer_class = BookSerializer

class BookDeleteApiView(APIView):

    def delete(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
            book.delete()
            return Response(
                {"status": "true",
                 "message": "Book deleted successfully"}, status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"status": "Error",
                 "message": "Book not found"}, status=status.HTTP_400_BAD_REQUEST
            )

#class BookUpdateApiView(generics.UpdateAPIView):
#    queryset = Book.objects.all()
#   serializer_class = BookSerializer

class BookUpdateApiView(APIView):

    def put(self, request, pk):
            book = Book.objects.get(id=pk)
            data = request.data
            serializer = BookSerializer(instance=book, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                book_saved=serializer.save()
                return Response(
                    {
                    "status": True,
                    "message": f"Book {book_saved} updated successfully",
                }
                )
            else:
                return Response({
                    "status": "Error",
                    "message": "Serializer is not valid"
                }
            )

#   class BookCreateApiView(generics.CreateAPIView):
#       queryset = Book.objects.all()
#       serializer_class = BookSerializer

class BookCreateApiView(APIView):

    def post(self, request):
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = {"Status": f"Book created successfully",
                    "books": data
                    }
            return Response(data)
        else:
            return Response(
                {"status": "Error",
                 "message": "Serializer is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )

class BookListCreateApiView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewset(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer