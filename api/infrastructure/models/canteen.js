const { DataTypes } = require('sequelize');
const { sequelize } = require('../postgres-database');

exports.Canteen = sequelize.define('canteen', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    unique: true,
    autoIncrement: true,
    allowNull: false
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  city: {
    type: DataTypes.STRING,
    allowNull: false
  },
  sector: {
    type: DataTypes.STRING,
    allowNull: false
  },
  hasPublished: {
    type: DataTypes.BOOLEAN,
    defaultValue: false,
  },
  dataIsPublic: {
    type: DataTypes.BOOLEAN,
    defaultValue: false,
  },
});
