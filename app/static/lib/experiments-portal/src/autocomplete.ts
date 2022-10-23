type SelectionEventHandler = (option: string) => void

function appendDropdownOption(dropdownElement: HTMLUListElement, option: string, onSelection: SelectionEventHandler, btnId?: string) {
  const listItem = document.createElement('li');
  listItem.classList.add('show');
  const button = document.createElement('button');
  button.addEventListener('click', () => onSelection(option));
  button.innerText = option;
  button.type = 'button';
  if (btnId) button.id = btnId;
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

export function addAutocomplete() {
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

  const handleSelection: SelectionEventHandler = (option) => { // Should refactor
    target.value = option;
    dropdownElement.classList.remove('show');
  };

  const getButtonId = (inputName: string) => `${inputName}-dropdown-btn`;

  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.type === 'attributes' && mutation.target.nodeName === 'INPUT') {
        const inputText = (mutation.target as HTMLInputElement).value;
        const buttonId = getButtonId(mutation.target.name);
        const button = document.getElementById(buttonId);
        if (button) {
          button.innerText = inputText;
        } else {
          appendDropdownOption(dropdownElement, inputText, handleSelection, buttonId);
        }
      } else if (mutation.type === 'childList' && mutation.removedNodes.length === 1) {
        const inputElementName = mutation.removedNodes.item(0)?.firstChild?.name;
        inputElementName && document.getElementById(getButtonId(inputElementName))?.remove();
      }
    }
  });

  observer.observe(source, {
    attributes: true,
    childList: true,
    subtree: true
  });

}