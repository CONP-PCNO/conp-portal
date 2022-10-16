import Freezeframe from 'freezeframe';

export function animateGifs() {
  const gifs = document.getElementsByClassName('animated-gif');
  new Freezeframe(gifs, {
    trigger: 'hover'
  });
}