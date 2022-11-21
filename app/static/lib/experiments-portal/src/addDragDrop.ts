import Dropzone from 'dropzone';

function getToken() {
  const input = document.getElementById('csrf_token');
  if (!input) {
    throw new Error('Input element with CSRF token does not exist');
  }
  return (input as HTMLInputElement).value;
}

export function addDragDrop() {
  const token = getToken();
  new Dropzone('#repository', {
    url: '/experiments/submit',
    headers: {
      'X-CSRFTOKEN': token
    },
    acceptedFiles: 'application/zip',
    paramName: 'repository'
  });
  new Dropzone('#image_file', {
    url: '/experiments/submit',
    headers: {
      'X-CSRFTOKEN': token
    },
    acceptedFiles: 'image/*',
    paramName: 'image_file'
  });
}
