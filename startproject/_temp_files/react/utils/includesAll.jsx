export default function includesAll(supersetArray, subsetArray) {
  return (subsetArray || []).every(function (item) {
    return supersetArray.indexOf(item) !== -1;
  });
}
