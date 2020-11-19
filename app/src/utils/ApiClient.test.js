import register from './ApiClient.js';

function setupFetchStub(data) {
    return function fetchStub(_url) {
      return Promise.resolve({
        json: () => Promise.resolve({message: data}),
      })
    }
}

test('calls register endpoint', async () => {
    const mockFn = jest.spyOn(global, "fetch").mockImplementation(setupFetchStub("User already registered"));
    register("mockToken");
    expect(mockFn).toHaveBeenCalledTimes(1);
    global.fetch.mockClear();
});