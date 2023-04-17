const PAGE_LOADER_ANIMATIONS = ['', 'is-bottom-to-top', 'is-right-to-left', 'is-left-to-right']

function setPageLoading(state, animation = PAGE_LOADER_ANIMATIONS[0], title = 'Načítání stránky...') {
    const pageLoader = document.getElementById('pageloader');
    const pageLoaderTitle = document.getElementById('pageloader-title');
    pageLoader.classList.toggle('is-active', state);
    if (animation && PAGE_LOADER_ANIMATIONS.includes(animation)) pageLoader.classList.add(animation);
    pageLoaderTitle.innerHTML = title;
}

function anchorPageLoad(a, animation = PAGE_LOADER_ANIMATIONS[0], title = 'Načítání stránky...') {
    if (a.href === window.location.href) return;
    setPageLoading(true, animation, title);
}