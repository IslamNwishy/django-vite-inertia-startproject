export default function Switch(props) {
  if (props.plain) return <input {...props} />;

  return (
    <label className="relative inline-flex items-center cursor-pointer">
      <input
        {...props}
        className="sr-only peer"
        onChange={(e) => {
          props.onChange({ target: { value: e.target.checked } });
        }}
        checked={props.value}
      />
      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-yellow-300 dark:peer-focus:ring-yellow-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-yellow-600"></div>
    </label>
  );
}
