type SelectionEventHandler = (option: string) => void

function appendDropdownOption(dropdownElement: HTMLUListElement, option: string, onSelection: SelectionEventHandler) {
  const listItem = document.createElement('li');
  listItem.classList.add('show');
  const button = document.createElement('button');
  button.addEventListener('click', () => onSelection(option));
  button.innerText = option;
  button.type = 'button';
  listItem.appendChild(button);
  dropdownElement.appendChild(listItem);
}

function createDropdownElement(options: string[], onSelection: SelectionEventHandler) {
  const dropdownElement = document.createElement('ul');
  dropdownElement.className = 'autocomplete-dropdown';
  options.forEach(option => {
    appendDropdownOption(dropdownElement, option, onSelection);
  });
  return dropdownElement;
}

export function setAutocompleteForInputElement(element: HTMLInputElement, options: string[]) {

  const handleSelection: SelectionEventHandler = (option) => {
    element.value = option;
    dropdownElement.classList.remove('show');
  };
  const dropdownElement = createDropdownElement(options, handleSelection);
  element.insertAdjacentElement('afterend', dropdownElement);

  element.addEventListener('focus', () => {
    dropdownElement.classList.add('show');
    window.addEventListener('click', (event) => {
      const target = event.target as HTMLElement;
      if (!(element.contains(target) || dropdownElement.contains(target))) {
        dropdownElement.classList.remove('show');
      }
    });
  });

  element.addEventListener('input', (event) => {
    Array.from(dropdownElement.children).forEach((child) => {
      const button = child.children.item(0) as HTMLButtonElement;
      const target = event.target as HTMLInputElement;
      const isMatch = button.innerText.toUpperCase().includes(target.value.toUpperCase());
      isMatch ? child.classList.add('show') : child.classList.remove('show');
    });
  });

}

function setAutocompleteForListElement(element: HTMLUListElement, options: string[]) {
  element.querySelectorAll('input').forEach(e => setAutocompleteForInputElement(e, options));
}

export function autocomplete() {
  const elements = document.querySelectorAll('.autocomplete[data-autocomplete]');
  for (let i = 0; i < elements.length; i++) {
    const element = elements.item(i) as HTMLElement;
    const data = element.getAttribute('data-autocomplete');
    if (data && element.nodeName == 'INPUT') {
      setAutocompleteForInputElement(element as HTMLInputElement, JSON.parse(data));
    } else if (data && element.nodeName == 'UL') {
      setAutocompleteForListElement(element as HTMLUListElement, JSON.parse(data));
    }
  }
}

export function suggestFromOtherField(targetId: string, sourceId: string) {

  const target = document.getElementById(targetId) as HTMLInputElement;
  const source = document.getElementById(sourceId) as HTMLUListElement;

  const sources: { [key: string]: string } = {};
  setAutocompleteForInputElement(target, Object.values(sources));

  const dropdownElement = target.parentElement?.querySelector('.autocomplete-dropdown') as HTMLUListElement;

  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.target.nodeName === 'INPUT') {
        sources[mutation.target.name] = (mutation.target as HTMLInputElement).value;
        /*
          check if target name is in dropdown options
            if yes, then modify
            else append new entry
          
        target.childNodes.forEach(node => console.log(node));
        appendDropdownOption(dropdownElement, sources[mutation.target.name], (option) => {
          target.value = option;
          dropdownElement.classList.remove('show');
        });
        */
      }
    }
  });

  observer.observe(source, {
    attributes: true,
    subtree: true
  });

  target.onfocus = () => {
    console.log(sources);
  };

  
  
  // observer.disconnect();

  /*
  const target = document.getElementById(targetId) as HTMLInputElement;
  const sourceField = document.getElementById(sourceFieldId) as HTMLUListElement;
  sourceField.lastElementChild?.addEventListener('blur', () => {
    if (target.nextElementSibling?.className === 'autocomplete-dropdown') {
      target.nextElementSibling.remove();
    }
    const inputSources = Array.from(sourceField.querySelectorAll('input')).map(e => e.value).filter(e => e);
    setAutocompleteForInputElement(target, inputSources);
  }); */
  // console.log(target);
  //const dropdownElement = target.parentElement?.querySelector('.autocomplete-dropdown') as HTMLElement;

}