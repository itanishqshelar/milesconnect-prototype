"use client";

interface NotificationsPanelProps {
    isOpen: boolean;
    onClose: () => void;
}

// Mock notifications - in a real app, these would come from a backend/state management
const mockNotifications = [
    {
        id: "1",
        type: "success" as const,
        title: "Shipment Delivered",
        message: "SHP-2024-001 was successfully delivered",
        time: "5 minutes ago",
        read: false,
    },
    {
        id: "2",
        type: "warning" as const,
        title: "Maintenance Due",
        message: "Vehicle MH-01-AB-1234 requires service",
        time: "1 hour ago",
        read: false,
    },
    {
        id: "3",
        type: "info" as const,
        title: "New Driver Onboarded",
        message: "John Doe has been added to the system",
        time: "2 hours ago",
        read: true,
    },
    {
        id: "4",
        type: "error" as const,
        title: "Payment Overdue",
        message: "Invoice INV-2024-045 is 3 days overdue",
        time: "1 day ago",
        read: true,
    },
];

export function NotificationsPanel({ isOpen, onClose }: NotificationsPanelProps) {
    if (!isOpen) return null;

    const unreadCount = mockNotifications.filter(n => !n.read).length;

    return (
        <>
            {/* Backdrop */}
            <button
                type="button"
                className="fixed inset-0 z-40 cursor-default"
                aria-label="Close notifications"
                onClick={onClose}
            />

            {/* Panel */}
            <div className="fixed right-4 top-16 z-50 w-96 max-h-[600px] transform rounded-xl border border-border bg-card shadow-2xl ring-1 ring-black/5 transition-all overflow-hidden">
                {/* Header */}
                <div className="flex items-center justify-between border-b border-border bg-muted/50 px-4 py-3">
                    <div>
                        <h3 className="font-semibold text-foreground">Notifications</h3>
                        {unreadCount > 0 && (
                            <p className="text-xs text-muted-foreground">{unreadCount} unread</p>
                        )}
                    </div>
                    <button
                        onClick={onClose}
                        className="rounded-md p-1 text-muted-foreground hover:bg-muted hover:text-foreground"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            strokeWidth={2}
                            stroke="currentColor"
                            className="w-4 h-4"
                        >
                            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                {/* Notifications List */}
                <div className="max-h-[500px] overflow-y-auto">
                    {mockNotifications.length === 0 ? (
                        <div className="p-8 text-center">
                            <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-muted">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    strokeWidth={1.5}
                                    stroke="currentColor"
                                    className="w-6 h-6 text-muted-foreground"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0"
                                    />
                                </svg>
                            </div>
                            <p className="text-sm text-muted-foreground">No notifications</p>
                        </div>
                    ) : (
                        <div className="divide-y divide-border">
                            {mockNotifications.map((notification) => (
                                <div
                                    key={notification.id}
                                    className={`p-4 hover:bg-muted/50 transition-colors cursor-pointer ${!notification.read ? "bg-primary/5" : ""
                                        }`}
                                >
                                    <div className="flex gap-3">
                                        <div className="flex-shrink-0">
                                            {notification.type === "success" && (
                                                <div className="h-8 w-8 rounded-full bg-green-100 dark:bg-green-950/30 flex items-center justify-center">
                                                    <svg
                                                        className="h-4 w-4 text-green-600 dark:text-green-400"
                                                        fill="none"
                                                        viewBox="0 0 24 24"
                                                        stroke="currentColor"
                                                    >
                                                        <path
                                                            strokeLinecap="round"
                                                            strokeLinejoin="round"
                                                            strokeWidth={2}
                                                            d="M5 13l4 4L19 7"
                                                        />
                                                    </svg>
                                                </div>
                                            )}
                                            {notification.type === "warning" && (
                                                <div className="h-8 w-8 rounded-full bg-amber-100 dark:bg-amber-950/30 flex items-center justify-center">
                                                    <svg
                                                        className="h-4 w-4 text-amber-600 dark:text-amber-400"
                                                        fill="none"
                                                        viewBox="0 0 24 24"
                                                        stroke="currentColor"
                                                    >
                                                        <path
                                                            strokeLinecap="round"
                                                            strokeLinejoin="round"
                                                            strokeWidth={2}
                                                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                                                        />
                                                    </svg>
                                                </div>
                                            )}
                                            {notification.type === "info" && (
                                                <div className="h-8 w-8 rounded-full bg-blue-100 dark:bg-blue-950/30 flex items-center justify-center">
                                                    <svg
                                                        className="h-4 w-4 text-blue-600 dark:text-blue-400"
                                                        fill="none"
                                                        viewBox="0 0 24 24"
                                                        stroke="currentColor"
                                                    >
                                                        <path
                                                            strokeLinecap="round"
                                                            strokeLinejoin="round"
                                                            strokeWidth={2}
                                                            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                                                        />
                                                    </svg>
                                                </div>
                                            )}
                                            {notification.type === "error" && (
                                                <div className="h-8 w-8 rounded-full bg-red-100 dark:bg-red-950/30 flex items-center justify-center">
                                                    <svg
                                                        className="h-4 w-4 text-red-600 dark:text-red-400"
                                                        fill="none"
                                                        viewBox="0 0 24 24"
                                                        stroke="currentColor"
                                                    >
                                                        <path
                                                            strokeLinecap="round"
                                                            strokeLinejoin="round"
                                                            strokeWidth={2}
                                                            d="M6 18L18 6M6 6l12 12"
                                                        />
                                                    </svg>
                                                </div>
                                            )}
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <div className="flex items-start justify-between gap-2">
                                                <p className="text-sm font-medium text-foreground">{notification.title}</p>
                                                {!notification.read && (
                                                    <span className="flex-shrink-0 h-2 w-2 rounded-full bg-primary" />
                                                )}
                                            </div>
                                            <p className="mt-1 text-sm text-muted-foreground line-clamp-2">
                                                {notification.message}
                                            </p>
                                            <p className="mt-1 text-xs text-muted-foreground">{notification.time}</p>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Footer */}
                {mockNotifications.length > 0 && (
                    <div className="border-t border-border bg-muted/50 px-4 py-2 text-center">
                        <button className="text-xs font-medium text-primary hover:underline">
                            View all notifications
                        </button>
                    </div>
                )}
            </div>
        </>
    );
}
