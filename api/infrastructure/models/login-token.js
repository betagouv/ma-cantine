const { DataTypes } = require('sequelize');
const { sequelize } = require('../postgres-database');
const { User } = require('./user');

const EXPIRE_MINUTES = 60;
const MILLISECONDS_IN_MINUTE = 60000;

exports.LoginToken = sequelize.define('LoginToken', {
  token: {
    type: DataTypes.STRING,
    primaryKey: true,
    unique: true,
    allowNull: false
  },
  userId: {
    type: DataTypes.INTEGER,
    allowNull: false,
    unique: true,
    references: {
      model: User,
      key: 'id'
    }
  },
  expirationDate: {
    type: DataTypes.VIRTUAL,
    get() {
      const tokenCreated = new Date(this.createdAt);
      return new Date(tokenCreated.getTime() + (EXPIRE_MINUTES * MILLISECONDS_IN_MINUTE));
    }
  }
});
