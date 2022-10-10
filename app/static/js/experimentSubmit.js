const addFieldListEntry = (fieldListId) => {
  const fieldList = document.getElementById(fieldListId);
  const listItems = fieldList.getElementsByTagName('li');
  const newListItem = document.createElement('li');
  const newInput = document.createElement('input');
  newInput.classList.add('form-control')
  fieldList.appendChild(newListItem);
  newListItem.appendChild(newInput);
}

const removeFieldListEntry = (fieldListId) => {
  const fieldList = document.getElementById(fieldListId);
  const listItems = fieldList.getElementsByTagName('li');
  if (listItems.length !== 1) {
    fieldList.removeChild(listItems.item(listItems.length - 1))
  }
}