export default function Select(props) {
  return (
    <select
      {...props}
      {...(props.multiple
        ? {
            onChange: (e) =>
              props.onChange({ target: { value: Array.from(e.target.selectedOptions).map((option) => option.value) } }),
          }
        : {})}
    >
      {props.choices.map((choice, index) => (
        <option value={choice[0]} key={index}>
          {choice[1]}
        </option>
      ))}
    </select>
  );
}
