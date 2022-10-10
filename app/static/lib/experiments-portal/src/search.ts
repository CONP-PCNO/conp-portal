export const handleSubmitSearch = (event: SubmitEvent) => {
  event.preventDefault();
  if (event.target) {
    const data = new FormData(event.target as HTMLFormElement);
    const url = new URL(document.location.href);
    const searchTerm = data.get('search_term');
    if (searchTerm) {
      url.searchParams.set('search_term', searchTerm.toString());
    } else {
      console.error('Search term is null, which should never happen!');
    }
    url.searchParams.set('page', '1');
    window.location.href = url.toString();
  }
};

export const handleCheckboxChange = (event: Event) => {
  const url = new URL(document.location.href);
  if (event.target) {
    const target = event.target as HTMLInputElement;
    const filters = url.searchParams.get(target.name)?.split(',');
    if (filters) {
      if (filters.includes(target.value)) {
        filters.splice(filters.indexOf(target.value), 1);
      } else {
        filters.push(target.value);
      }
      const newValue = filters.join(',');
      if (newValue) {
        url.searchParams.set(target.name, newValue);
      } else {
        url.searchParams.delete(target.name);
      }
    } else {
      url.searchParams.append(target.name, target.value);
    }
    url.searchParams.set('page', '1');
    window.location.href = url.toString();
  }
};

export const handlePageChange = (pageNumber: number | string) => {
  const url = new URL(document.location.href);
  url.searchParams.set('page', pageNumber.toString());
  window.location.href = url.toString();
};

export const updateSearchParam = (key: string, value: string) => {
  const url = new URL(document.location.href);
  url.searchParams.set(key, value);
  url.searchParams.set('page', '1');
  window.location.href = url.toString();
};
