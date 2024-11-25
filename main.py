from fastapi import FastAPI, HTTPException
from models import ItemPayload

app = FastAPI()

# a new empty dictionary which receives keys of type int (item IDs) and values of ItemPayload
grocery_list: dict[int, ItemPayload] = {}

# route defined below: when a client sends a request to this endpoint, FastAPI routes the request to the route handler/view function which then generates a response
@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello Natasha"}

# route to add an item
@app.post("/items/{item_name}/{quantity}")
def add_item(item_name: str, quantity: int) -> dict[str, ItemPayload]:
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0.")
    
    # get all item names
    # the following line creates a dictionary (item_ids) which maps item names to item IDs, iterating over items in grocery_list
    # it checks if the id is not none, if it is, it uses the default value of 0
    items_ids: dict[str, int] = {item.item_name: item.item_id if item.item_id is not None else 0 for item in grocery_list.values()}
    
    # if item already exists, add the quantity
    if item_name in items_ids.keys():
        # get index of item_name in item_ids, which is the item_id
        item_id = items_ids[item_name]
        # then access the existing item in grocery_list and increase the quantity
        grocery_list[item_id].quantity += quantity

    # otherwise, create a new item
    else:
        # generate an ID for the item based on the highest ID in the grocery_list
        # max() finds the highest id in the list and then it assigns one higher to the new item
        # if grocery list is empty - assign item_id to 0
        item_id: int = max(grocery_list.keys()) + 1 if grocery_list else 0
        # adds a new item to grocery_list using the new item_id and creating a new instance of ItemPayload
        grocery_list[item_id] = ItemPayload(
            item_id=item_id, item_name=item_name, quantity=quantity
        )
    
    # return a JSON response with the newly added or updated item - FastAPI automatically serializes the ItemPayload object into a JSON format for the response
    return {"item": grocery_list[item_id]}

# Route to list a specific item by ID
@app.get("/items/{item_id}")
def list_item(item_id: int) -> dict[str, ItemPayload]:
    if item_id not in grocery_list:
        raise HTTPException(status_code=404, detail="Item not found.")
    return {"item": grocery_list[item_id]}

# Route to list all items
@app.get("/items")
def list_items() -> dict[str, dict[int, ItemPayload]]:
    return {"items": grocery_list}

# Route to delete a specific item by ID
@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, str]:
    if item_id not in grocery_list:
        raise HTTPException(status_code=404, detail="Item not found.")
    del grocery_list[item_id]
    return {"result": "Item deleted."}

# Route to remove some quantity of a specific item by ID
@app.delete("items/{item_id}/{quantity}")
def remove_quantity(item_id: int, quantity: int) -> dict[str, str]:
    if item_id not in grocery_list:
        raise HTTPException(status_code=404, detail="Item not found.")
    # if quantity to be removed is higher or equal to item's quantity, delete the item
    if grocery_list[item_id].quantity <= quantity:
        del grocery_list[item_id]
        return {"result": "Item deleted."}
    else:
        grocery_list[item_id].quantity -= quantity
    # 'f' denotes string interpolation in Python
    return {"result": f"{quantity} items removed."}