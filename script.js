/* A foto continua acessível por link quando JavaScript não está disponível. */
const portraitLink = document.getElementById('portrait-link');
const portraitDialog = document.getElementById('portrait-dialog');
const closeDialog = document.getElementById('close-dialog');

if (portraitLink && portraitDialog && typeof portraitDialog.showModal === 'function') {
  portraitLink.setAttribute('aria-haspopup', 'dialog');
  portraitLink.addEventListener('click', (event) => {
    event.preventDefault();
    portraitDialog.showModal();
  });
  closeDialog.addEventListener('click', () => portraitDialog.close());
  portraitDialog.addEventListener('click', (event) => {
    if (event.target === portraitDialog) {
      const box = portraitDialog.getBoundingClientRect();
      if (event.clientX < box.left || event.clientX > box.right ||
          event.clientY < box.top || event.clientY > box.bottom) portraitDialog.close();
    }
  });
  portraitDialog.addEventListener('close', () => portraitLink.focus());
}
