
import { cn } from "@/lib/utils";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Upload, FileText, Shield, Lightbulb, ChevronsLeft, ChevronsRight } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

type SidebarItem = {
  title: string;
  icon: React.ElementType;
  path: string;
};

const sidebarItems: SidebarItem[] = [
  {
    title: "Upload",
    icon: Upload,
    path: "#upload",
  },
  {
    title: "Review",
    icon: FileText,
    path: "#review",
  },
  {
    title: "Risks",
    icon: Shield,
    path: "#risks",
  },
  {
    title: "Suggestions",
    icon: Lightbulb,
    path: "#suggestions",
  },
  {
    title: "Summary",
    icon: FileText,
    path: "#summary",
  },
];

interface SidebarProps {
  activeItem: string;
  setActiveItem: (path: string) => void;
}

export function Sidebar({ activeItem, setActiveItem }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  
  // Check if we're in mobile view
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
      // On mobile, default to collapsed
      if (window.innerWidth < 768) {
        setCollapsed(true);
      }
    };
    
    // Initial check
    checkMobile();
    
    // Listen for resize events
    window.addEventListener('resize', checkMobile);
    
    // Cleanup
    return () => window.removeEventListener('resize', checkMobile);
  }, []);
  
  // Function to toggle sidebar collapsed state
  const toggleSidebar = () => {
    setCollapsed(!collapsed);
  };

  // Handle item click
  const handleItemClick = (path: string) => {
    setActiveItem(path);
    window.location.hash = path.replace('#', '');
    
    // On mobile, collapse the sidebar after a selection
    if (isMobile) {
      setCollapsed(true);
    }
  };

  // Sidebar animation variants
  const sidebarVariants = {
    expanded: { width: "16rem", transition: { duration: 0.3 } },
    collapsed: { width: "4rem", transition: { duration: 0.3 } },
  };

  return (
    <motion.div
      initial={{ x: -10, opacity: 0 }}
      animate={{ 
        x: 0, 
        opacity: 1,
        width: collapsed ? "4rem" : "16rem"
      }}
      variants={sidebarVariants}
      transition={{ duration: 0.3, delay: 0.1 }}
      className={cn(
        "h-screen sticky top-0 flex flex-col bg-sidebar border-r border-sidebar-border z-40"
      )}
    >
      <div className="flex items-center justify-between h-14 px-4 border-b border-sidebar-border">
        <AnimatePresence>
          {!collapsed && (
            <motion.h2 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="font-heading font-semibold text-lg text-sidebar-foreground"
            >
              LegalAI
            </motion.h2>
          )}
        </AnimatePresence>
        <Button
          variant="ghost"
          size="icon"
          className="ml-auto text-sidebar-foreground"
          onClick={toggleSidebar}
        >
          {collapsed ? (
            <ChevronsRight className="h-4 w-4" />
          ) : (
            <ChevronsLeft className="h-4 w-4" />
          )}
        </Button>
      </div>
      <div className="flex-1 overflow-y-auto py-4">
        <nav className="grid gap-1 px-2">
          {sidebarItems.map((item) => (
            <motion.div
              key={item.path}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <Button
                variant={activeItem === item.path ? "secondary" : "ghost"}
                className={cn(
                  "w-full flex items-center justify-start gap-3 h-10 px-4 py-2 text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
                  activeItem === item.path && "bg-sidebar-accent text-sidebar-accent-foreground",
                  collapsed && "justify-center px-0"
                )}
                onClick={() => handleItemClick(item.path)}
              >
                <item.icon className="h-5 w-5" />
                <AnimatePresence>
                  {!collapsed && (
                    <motion.span
                      initial={{ opacity: 0, width: 0 }}
                      animate={{ opacity: 1, width: "auto" }}
                      exit={{ opacity: 0, width: 0 }}
                      transition={{ duration: 0.2 }}
                    >
                      {item.title}
                    </motion.span>
                  )}
                </AnimatePresence>
              </Button>
            </motion.div>
          ))}
        </nav>
      </div>
    </motion.div>
  );
}
