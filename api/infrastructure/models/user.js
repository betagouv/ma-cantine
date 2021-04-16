// For some reason, removing the unused Sequelize from here causes the tests to break
const { Sequelize, DataTypes } = require('sequelize');
const { sequelize } = require('../postgres-database');

exports.User = sequelize.define('User', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    unique: true,
    autoIncrement: true,
    allowNull: false
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    validate: {
      isEmail: {
        msg: "Must be a valid email address"
      }
    }
  },
  firstName: {
    type: DataTypes.STRING,
    allowNull: false
  },
  lastName: {
    type: DataTypes.STRING,
    allowNull: false
  },
  canteenId: {
    type: DataTypes.INTEGER,
    allowNull: false,
  }
});