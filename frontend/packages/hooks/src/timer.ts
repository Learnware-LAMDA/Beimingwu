import { ref, Ref } from "vue";

export function useTimeout(delay: number): {
  ok: Ref<boolean>;
  remain: Ref<number>;
  start: () => void;
  stop: () => void;
} {
  const ok = ref<boolean>(true);
  const remain = ref<number>(delay);
  const timeout = ref<number>(0);
  const timer = ref<number>(0);

  function start(): void {
    ok.value = false;
    remain.value = delay;
    timeout.value = Number(
      setTimeout(() => {
        ok.value = true;
        clearInterval(timer.value);
      }, delay),
    );
    timer.value = Number(
      setInterval(() => {
        remain.value -= 1000;
      }, 1000),
    );
  }

  function stop(): void {
    ok.value = false;
    clearTimeout(timer.value);
    clearInterval(timeout.value);
  }

  return {
    ok,
    remain,
    start,
    stop,
  };
}
