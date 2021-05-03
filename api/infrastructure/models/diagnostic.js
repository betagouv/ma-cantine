const { DataTypes } = require('sequelize');
const { sequelize } = require('../postgres-database');
const { Canteen } = require('./canteen');

let Diagnostic = sequelize.define('diagnostic', {
  year: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    allowNull: false
  },
  valueBio: DataTypes.FLOAT,
  valueFairTrade: DataTypes.FLOAT,
  valueSustainable: DataTypes.FLOAT,
  valueTotal: DataTypes.FLOAT,
  hasMadeWasteDiagnostic: DataTypes.BOOLEAN,
  hasMadeWastePlan: DataTypes.BOOLEAN,
  wasteActions: DataTypes.ARRAY(DataTypes.STRING),
  hasDonationAgreement: DataTypes.BOOLEAN,
  hasMadeDiversificationPlan: DataTypes.BOOLEAN,
  vegetarianFrequency: DataTypes.STRING,
  vegetarianMenuType: DataTypes.STRING,
  cookingFoodContainersSubstituted: DataTypes.BOOLEAN,
  serviceFoodContainersSubstituted: DataTypes.BOOLEAN,
  waterBottlesSubstituted: DataTypes.BOOLEAN,
  disposableUtensilsSubstituted: DataTypes.BOOLEAN,
  communicationSupport: DataTypes.ARRAY(DataTypes.STRING),
  communicationSupportLink: DataTypes.STRING,
  communicateOnFoodPlan: DataTypes.BOOLEAN
});

Canteen.hasMany(Diagnostic, {
  foreignKey: {
    primaryKey: true,
    allowNull: false // diagnostic must be associated with a canteen
  }
});

Diagnostic.belongsTo(Canteen);

exports.Diagnostic = Diagnostic;