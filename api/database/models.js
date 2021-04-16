// For some reason, removing the unused Sequelize from here causes the tests to break
const { Sequelize, DataTypes } = require('sequelize');
const { sequelize } = require('./setup');

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

exports.Canteen = sequelize.define('Canteen', {
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
  // TODO: validate department and sector input
  department: {
    type: DataTypes.STRING,
    allowNull: false
  },
  sector: {
    type: DataTypes.STRING,
    allowNull: false
  }
});
