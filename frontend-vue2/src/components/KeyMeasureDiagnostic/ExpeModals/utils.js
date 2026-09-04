export const treatOutboundPercentageValues = function(payload, percentageFields) {
  for (let i = 0; i < percentageFields.length; i++) {
    if (Object.prototype.hasOwnProperty.call(payload, percentageFields[i]))
      payload[percentageFields[i]] = parseFloat((payload[percentageFields[i]] / 100).toPrecision(3))
  }
  return payload
}
export const treatInboundPercentageValues = function(expe, percentageFields) {
  for (let i = 0; i < percentageFields.length; i++) {
    if (Object.prototype.hasOwnProperty.call(expe, percentageFields[i]))
      expe[percentageFields[i]] = parseFloat((expe[percentageFields[i]] * 100).toPrecision(4))
  }
  return expe
}
