export const addFieldListEntry = (fieldListId: string) => {
  const fieldList = document.getElementById(fieldListId);
  if (fieldList) {
    const listItems = fieldList.getElementsByTagName('li');
    const newListItem = document.createElement('li');
    const newInput = document.createElement('input');
    const newInputName = `${fieldListId}-${listItems.length}`;
    newInput.classList.add('form-control');
    newInput.name = newInputName;
    newInput.id = newInputName;
    fieldList.appendChild(newListItem);
    newListItem.appendChild(newInput);
  } else {
    console.error(`Element does not exist: ${fieldListId}`);
  }
};

export const removeFieldListEntry = (fieldListId: string) => {
  const fieldList = document.getElementById(fieldListId);
  if (fieldList) {
    const listItems = fieldList.getElementsByTagName('li');
    if (listItems.length !== 1) {
      fieldList.removeChild(listItems.item(listItems.length - 1) as HTMLElement);
    }
  } else {
    console.error(`Element does not exist: ${fieldListId}`);
  }
};