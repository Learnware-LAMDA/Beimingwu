function debounce(fn: (...args: unknown[]) => void, delay: number): (...args: unknown[]) => void {
  let timer: number | null = null;
  return function (...args: unknown[]) {
    if (timer) clearTimeout(timer);
    timer = Number(
      setTimeout(function () {
        fn(...args);
      }, delay),
    );
  };
}

function throttle(fn: (...args: unknown[]) => void, delay: number): (...args: unknown[]) => void {
  let timer: number | null = null;
  return function (...args: unknown[]) {
    if (!timer) {
      timer = Number(
        setTimeout(function () {
          fn(...args);
          timer = null;
        }, delay),
      );
    }
  };
}

export { debounce, throttle };
