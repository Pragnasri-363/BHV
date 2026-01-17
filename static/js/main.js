
        function toggleNotificationPanel() {
                const panel = document.getElementById("notification-panel");
                const opening = panel.classList.contains("hidden");

                if (opening) {
                    panel.classList.remove("hidden");

                    
                    fetchNotifications();

                    
                    setTimeout(() => {
                        markAllAsSeen();
                    }, 500);
                } else {
                    panel.classList.add("hidden");
                }
            }

        function renderNotifications(targetId, data) {
                const listDiv = document.getElementById(targetId);
                const emptyDiv = document.getElementById("no-notifications");

                if (!Array.isArray(data) || data.length === 0) {
                    if (emptyDiv) emptyDiv.style.display = "flex";
                    return 0;
                }

                if (emptyDiv) emptyDiv.remove();

                listDiv.innerHTML = data.map(n => `
                    <div class="notification-item ${n.seen ? '' : 'unseen'}">
                        <div class="notification-title">${n.title}</div>
                        <div>${n.message}</div>
                        <div class="notification-time">
                            ${new Date(n.created_at).toLocaleString()}
                        </div>
                    </div>
                `).join('');

                return data.filter(n => !n.seen).length;
            }




        async function fetchNotifications() {
                const res = await fetch('/api/admin/notifications');

                const data = await res.json();

                const unread = renderNotifications("notifications-list-panel", data);
                document.getElementById("unread-count").textContent = unread;
            }




        async function markAllAsSeen() {
            try {
                await fetch('/api/admin/notifications/mark-seen', { method: 'POST'});
                fetchNotifications();
            } catch (err) {
                console.error('Error marking as seen:', err);
            }
        }

        fetchNotifications();
