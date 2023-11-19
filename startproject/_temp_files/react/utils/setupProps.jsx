import includesAll from './includesAll';

function getLastProps() {
  try {
    return JSON.parse(sessionStorage.getItem('lastProps'));
  } catch {
    return {};
  }
}

export default function setupProps(page) {
  const lastProps = getLastProps() || {};

  const extras = page.props?.__EXTRAS__;
  if (!extras) return page;

  page.extras = extras;
  if (extras?.stale) {
    page.props = { ...lastProps, ...page.props };
    if (!includesAll(Object.keys(lastProps), page.props.refresh_context_attrs)) {
      //fallback to full reload in case of missing props to the stale page for any reason
      window.location.href = window.location.href;
    }
  } else sessionStorage.setItem('lastProps', JSON.stringify(page.props));

  return page;
}
