import Freezeframe from 'freezeframe';

export const animateGifs = () => {
  const gifs = document.getElementsByClassName('animated-gif');
  new Freezeframe(gifs, {
    trigger: 'hover'
  });
};