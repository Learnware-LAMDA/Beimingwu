import { reactive, watch } from "vue";

interface Field<T> {
  value: T;
  errorMessages: string;
  valid: boolean;
}

export function useField<T>({
  defaultValue,
  defaultValid = false,
  validate = (): string => "",
}: {
  defaultValue: T;
  defaultValid?: boolean;
  validate?: (value: T) => string | Promise<string>;
}): Field<T> {
  const field = reactive<Field<T>>({
    value: defaultValue,
    errorMessages: "",
    valid: defaultValid,
  });

  watch(
    () => field.value,
    async (value) => {
      field.valid = false;
      const errorMessages = await validate(value as T);
      if (errorMessages === "") {
        field.errorMessages = "";
        field.valid = true;
      } else {
        field.errorMessages = errorMessages;
        field.valid = false;
      }
    },
  );

  return field as Field<T>;
}
