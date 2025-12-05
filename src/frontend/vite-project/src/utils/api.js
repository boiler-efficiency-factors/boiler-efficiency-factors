// API 유틸리티 함수

const API_BASE_URL = 'http://127.0.0.1:8000/api'

// 인증된 요청을 위한 헤더 가져오기
export const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token')
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : '',
  }
}

// 토큰 갱신
export const refreshAccessToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token')
  
  if (!refreshToken) {
    throw new Error('No refresh token available')
  }

  try {
    const response = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        refresh: refreshToken,
      }),
    })

    if (response.ok) {
      const data = await response.json()
      localStorage.setItem('access_token', data.access)
      return data.access
    } else {
      throw new Error('Token refresh failed')
    }
  } catch (error) {
    // 토큰 갱신 실패 시 로그아웃
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('username')
    window.location.href = '/'
    throw error
  }
}

// 인증된 API 요청
export const authenticatedFetch = async (url, options = {}) => {
  let headers = getAuthHeaders()
  
  try {
    let response = await fetch(`${API_BASE_URL}${url}`, {
      ...options,
      headers: {
        ...headers,
        ...options.headers,
      },
    })

    // 401 에러 시 토큰 갱신 후 재시도
    if (response.status === 401) {
      await refreshAccessToken()
      headers = getAuthHeaders()
      
      response = await fetch(`${API_BASE_URL}${url}`, {
        ...options,
        headers: {
          ...headers,
          ...options.headers,
        },
      })
    }

    return response
  } catch (error) {
    console.error('API request failed:', error)
    throw error
  }
}
