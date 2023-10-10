function debounce(fn, delay): (...args: unknown[]) => void {
  let timer = null;
  return function (...args: unknown[]) {
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn(...args)
    }, delay);
  };
}

function throttle(fn, delay): (...args: unknown[]) => void {
  let timer = null;
  return function (...args: unknown[]) {
    if (!timer) {
      timer = setTimeout(function () {
        fn(...args);
        timer = null;
      }, delay);
    }
  };
}

export { debounce, throttle };
