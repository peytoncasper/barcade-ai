export default function TweetList({ turns, agent }) {
    return (
        <div>
            <div className="border-b border-gray-200 bg-white px-4 py-5 sm:px-6">
                <h3 className="text-base font-semibold leading-6 text-gray-900">{agent}</h3>
            </div>

            <ul
                role="list"
                className="divide-y divide-gray-100 overflow-hidden bg-white shadow-sm ring-1 ring-gray-900/5 sm:rounded-xl"
            >
                {turns.map((turn,index) => (
                    <li key={index} className="relative flex justify-between gap-x-6 px-4 py-5 hover:bg-gray-50 sm:px-6">
                        <div className="flex gap-x-4">
                            <div className="min-w-0 flex-auto">
                                <p className="text-sm font-semibold leading-6 text-gray-900">
                                    <span className="absolute inset-x-0 -top-px bottom-0" />
                                    Turn {turns.length - index}
                                </p>
                                <p className="mt-1 flex text-xs leading-5 text-gray-500">
                                    {turn}
                                </p>
                            </div>
                        </div>

                    </li>
                ))}
            </ul>
        </div>
    )
}
