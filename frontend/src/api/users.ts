import { api } from './client'

export interface User {
  id: string
  username: string
  email: string
  is_active: boolean
  created_at: string
}

export interface UserList {
  items: User[]
  total: number
  limit: number
  offset: number
}

export interface UserCreate {
  username: string
  email: string
  password: string
}

export const usersApi = {
  list: (limit = 20, offset = 0) =>
    api.get<UserList>(`/v1/users?limit=${limit}&offset=${offset}`),

  get: (id: string) =>
    api.get<User>(`/v1/users/${id}`),

  create: (data: UserCreate) =>
    api.post<User>('/v1/users', data),
}
