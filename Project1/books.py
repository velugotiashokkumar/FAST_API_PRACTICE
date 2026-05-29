from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/api_endpoint")
async def endpoint():
    return {"message" : "Hello This is my first endpoint"}

@app.get("/books")
async def read_all_books():
    return BOOKS

#Path Parameters
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

#Query Parameters
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/author/")
async def get_books_by_author(author_search: str):
    books_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author_search.casefold():
            books_return.append(book)           
    return books_return


@app.get("/books/{book_author}/")
async def read_author_caegory_by_query(book_author: str, category: str):
    books_to_return = []
    for books in BOOKS:
        if books.get('author').casefold() == book_author.casefold() and \
            books.get('category').casefold() == category.casefold():
                books_to_return.append(books)
                
    return books_to_return


#Note: Get request cannot have a Body() and Post request should have a Body() This is how fastapi differs it.
# POST Request Method
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book) 


# PUT Request Method
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            
            
# DELETE Request Method
@app.delete("/books/delete_book/{book_title}")
async def delete(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break