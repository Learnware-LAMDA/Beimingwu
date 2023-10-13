import { reactive, watch } from "vue";

interface Field<T> {
  value: T;
  errorMessages: string;
  valid: boolean;
}

export function useField<T>(
  defaultValue: T,
  validate: (value: T) => string | Promise<string> = (): string => "",
): Field<T> {
  const field = reactive<Field<T>>({
    value: defaultValue,
    errorMessages: "",
    valid: false,
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
