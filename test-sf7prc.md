# Consistent Hashing

Consistent hashing is a distributed hashing technique that minimizes redistribution when nodes are added or removed from a system, making it ideal for caches and load balancers. Unlike traditional modulo-based hashing where most keys are remapped on node changes, consistent hashing uses a hash ring ensuring only affected keys are redistributed. This property is essential for maintaining performance and availability in large-scale systems with dynamic node membership.
