import { setAutocompleteForInputElement } from './autocomplete';

export function addFieldListEntry(fieldListId: string) {
  const fieldList = document.getElementById(fieldListId) as HTMLUListElement;
  const listItems = fieldList.children;
  const newListItem = document.createElement('li');
  const newInput = document.createElement('input');
  const newInputName = `${fieldListId}-${listItems.length}`;
  newInput.classList.add('form-control');
  newInput.name = newInputName;
  newInput.id = newInputName;
  fieldList.appendChild(newListItem);
  newListItem.appendChild(newInput);
  const autocompleteData = fieldList.getAttribute('data-autocomplete');
  if (autocompleteData) {
    setAutocompleteForInputElement(newInput, JSON.parse(autocompleteData));
  }
}

export function removeFieldListEntry(fieldListId: string) {
  const fieldList = document.getElementById(fieldListId);
  if (fieldList) {
    const listItems = fieldList.children;
    if (listItems.length !== 1) {
      fieldList.removeChild(listItems.item(listItems.length - 1) as HTMLElement);
    }
  } else {
    console.error(`Element does not exist: ${fieldListId}`);
  }
}

/*
export function suggestFromOtherField(event: MouseEvent, sourceFieldId: string) {

  const target = event.target as HTMLInputElement;
  const sourceField = document.getElementById(sourceFieldId) as HTMLUListElement;
  const data = sourceField.getAttribute('data-autocomplete');
  console.log(data);
  const target = event.target as HTMLInputElement;
  const sourceField = document.getElementById(sourceFieldId) as HTMLUListElement;
  if (!sourceField) {
    throw new Error(`Source element does not exist: ${sourceFieldId}`);
  } else if (!target) {
    throw new Error('Target element does not exist');
  }
  const inputElements = Array.from(sourceField.children).map(child => {
    if (child.children.length !== 1 || child.children.item(0)?.nodeName !== 'INPUT') {
      throw new Error('All children of source ul element must contain a single input element');
    }
    return child.children.item(0) as HTMLInputElement;
  });
  const dataList = document.createElement('datalist');
  const dataListId = `${target.id}-data-list`;
  dataList.id = dataListId;
  inputElements.forEach(element => {
    if (element.value) {
      const option = document.createElement('option');
      option.value = element.value;
      dataList.appendChild(option);
    }
  });
  target.setAttribute('list', dataListId);
  target.insertAdjacentElement('afterend', dataList);
  
}
*/