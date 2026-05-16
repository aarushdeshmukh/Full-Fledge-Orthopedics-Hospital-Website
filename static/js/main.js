// Scroll reveal
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((e,i) => {
    if(e.isIntersecting){
      setTimeout(()=>e.target.classList.add('visible'), i*80);
      revealObserver.unobserve(e.target);
    }
  });
}, {threshold:0.1});
document.querySelectorAll('.reveal').forEach(el=>revealObserver.observe(el));

// Hamburger
const hamburger = document.getElementById('hamburger');
const navLinks  = document.querySelector('.nav-links');
if(hamburger){
  hamburger.addEventListener('click',()=>navLinks.classList.toggle('open'));
}

// Navbar — always stays white, only shadow changes on scroll
const navbar = document.querySelector('.navbar');
if(navbar){
  window.addEventListener('scroll',()=>{
    navbar.style.background = 'rgba(255,255,255,0.98)';
    navbar.style.borderBottom = '1px solid #E2EAF4';
    if(window.scrollY > 60){
      navbar.style.boxShadow = '0 2px 20px rgba(30,111,217,0.1)';
    } else {
      navbar.style.boxShadow = '0 1px 12px rgba(30,111,217,0.06)';
    }
  });
}
