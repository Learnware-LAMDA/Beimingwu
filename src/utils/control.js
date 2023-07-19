function debounce(fn, delay) {
  let timer = null;
  return function () {
    const context = this;
    const args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, delay);
  };
}

function throttle(fn, delay) {
  let timer = null;
  return function () {
    const context = this;
    const args = arguments;
    if (!timer) {
      timer = setTimeout(function () {
        fn.apply(context, args);
        timer = null;
      }, delay);
    }
  };
}

export { debounce, throttle };
