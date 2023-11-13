export default function Radio(props) {
  const defaultClasses =
    'border border-gray-300 rounded-full text-brand-600 bg-white checked:bg-brand-600 checked:border-brand-600 focus:ring-brand-600';

  return (
    <div className="flex flex-row gap-2 items-center">
      <input
        id={props.label}
        {...props}
        type="radio"
        value={props.value}
        className={props.className || defaultClasses}
        onChange={(e) => {
          props.onChange({ target: { value: e.target.checked, label: props.label } });
        }}
        checked={props.checked}
      />
      <label htmlFor={props.label}>{props.label}</label>
    </div>
  );
}
