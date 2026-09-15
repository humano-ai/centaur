import { describe, expect, test } from 'bun:test'
import { assistantLoadingMessages } from '../src/index'

describe('assistantLoadingMessages', () => {
  const options = { assistantLoadingMessages: ['Warming up the forge...', 'Reading the thread...'] }

  test('rotates configured messages for the default thinking status', () => {
    expect(assistantLoadingMessages('Thinking...', 'Thinking...', options)).toEqual([
      'Warming up the forge...',
      'Reading the thread...'
    ])
  })

  test('keeps activity statuses as a single line', () => {
    expect(assistantLoadingMessages('Running tests', 'Running tests', options)).toEqual(['Running tests'])
  })

  test('falls back to the status itself and clears on empty', () => {
    expect(assistantLoadingMessages('Thinking...', 'Thinking...', {})).toEqual(['Thinking...'])
    expect(assistantLoadingMessages('', '', options)).toBeUndefined()
  })
})
