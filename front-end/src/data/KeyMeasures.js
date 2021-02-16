import keyMeasures from "@/data/key-measures.json";

function saveStatusesLocally() {
  let statuses = {};
  keyMeasures.forEach((measure) => {
    measure.subMeasures.forEach((subMeasure) => {
      if(subMeasure.status) {
        statuses[subMeasure.id] = subMeasure.status;
      }
    });
  });
  localStorage.setItem('statuses', JSON.stringify(statuses));
}

let statuses = localStorage.getItem('statuses') || "{}";
statuses = JSON.parse(statuses);

keyMeasures.forEach(measure => {
  measure.subMeasures.forEach(subMeasure => {
    subMeasure.status = statuses[subMeasure.id];
  });
});

export {
  keyMeasures,
  saveStatusesLocally
};