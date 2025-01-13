import api from '../../../shared/api.js'
import {BASE_ROUTE} from './constants.js'

export default class HackableService {
    async login(params) {
        return await api.POST(`${BASE_ROUTE}/login/`, params)
    }
    async createAccount(params) {
        return await api.POST(`${BASE_ROUTE}/createAccount/`, params)
    }
}
