// For some reason, removing the unused Sequelize from here causes the tests to break
const { Sequelize, DataTypes } = require('sequelize');
const { sequelize } = require('../postgres-database');
const { Canteen } = require('./canteen');

let User = sequelize.define('user', {
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
  }
});

Canteen.hasMany(User, {
  foreignKey: {
    allowNull: false // user must be associated with a canteen
  }
});

User.belongsTo(Canteen);

exports.User = User;