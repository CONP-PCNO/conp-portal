const handleSubmitSearch = (event) => {
  event.preventDefault()
  const data = new FormData(event.target);
  const url = new URL(document.location.href);
  url.searchParams.set('search_term', data.get('search_term'));
  url.searchParams.set('page', 1);
  window.location.href = url;
}

const handleCheckboxChange = (event) => {
  const url = new URL(document.location.href);
  if (url.searchParams.has(event.target.name)) {
    const filters = url.searchParams.get(event.target.name).split(',');
    if (filters.includes(event.target.value)) {
      filters.pop(event.target.value)
    } else {
      filters.push(event.target.value)
    }
    const newValue = filters.join(',');
    if (newValue) {
      url.searchParams.set(event.target.name, newValue)
    } else {
      url.searchParams.delete(event.target.name)
    }
  } else {
    url.searchParams.append(event.target.name, event.target.value)
  }
  url.searchParams.set('page', 1);
  window.location.href = url;
}

const handlePageChange = (pageNumber) => {
  const url = new URL(document.location.href)
  url.searchParams.set('page', pageNumber);
  window.location.href = url;
}

const updateSearchParam = (key, value) => {
  const url = new URL(document.location.href);
  url.searchParams.set(key, value);
  url.searchParams.set('page', 1);
  window.location.href = url;
}