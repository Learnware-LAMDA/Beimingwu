function debounce<T>(fn: (...args: T[]) => void, delay: number): (...args: T[]) => void {
  let timer: number | null = null;
  return function (...args: T[]) {
    if (timer) clearTimeout(timer);
    timer = Number(
      setTimeout(function () {
        fn(...args);
      }, delay),
    );
  };
}

function throttle<T>(fn: (...args: T[]) => void, delay: number): (...args: T[]) => void {
  let timer: number | null = null;
  return function (...args: T[]) {
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
